from django.db import transaction
from control_escolar.models import Pago, TipoPago
from django.utils import timezone


class PagoService:
    def __init__(self, inscripcion):
        self.inscripcion = inscripcion
        self.programa = inscripcion.campania_programa.programa
        self.duracion_meses = inscripcion.campania_programa.programa.duracion_meses

    def obtener_costos_reales(self):
        """Obtiene los costos considerando precios custom si existen"""
        return {
            'inscripcion': self.inscripcion.costo_inscripcion_acordado or self.programa.costo_inscripcion,
            'mensualidad': self.inscripcion.costo_mensualidad_acordado or self.programa.costo_mensualidad,
            'documentacion': self.inscripcion.costo_documentacion_acordado or self.programa.costo_documentacion
        }

    def calcular_total_diplomado(self):
        costos = self.obtener_costos_reales()
        return (
                costos['inscripcion'] +
                costos['documentacion'] +
                (costos['mensualidad'] * self.duracion_meses)
        )

    def crear_pago_inscripcion(self, estado, notas=None, fecha_pago=None):
        tipo_pago = TipoPago.objects.get(nombre="Inscripcion")
        costos = self.obtener_costos_reales()
        return Pago.objects.create(
            inscripcion=self.inscripcion,
            tipo_pago=tipo_pago,
            estado=estado,
            notas=notas,
            monto=costos['inscripcion'],
            fecha_pago=fecha_pago
        )

    def crear_pago_documentacion(self, estado, notas=None, fecha_pago=None):
        tipo_pago = TipoPago.objects.get(nombre="Documentacion")
        costos = self.obtener_costos_reales()
        return Pago.objects.create(
            inscripcion=self.inscripcion,
            tipo_pago=tipo_pago,
            estado=estado,
            notas=notas,
            monto=costos['documentacion'],
            fecha_pago=fecha_pago
        )

    def crear_pagos_mensualidades(self, estado, fecha_pago=None):
        tipo_pago = TipoPago.objects.get(nombre="Mensualidad")
        costos = self.obtener_costos_reales()
        pagos_creados = []

        for mes in range(1, self.duracion_meses + 1):
            pago = Pago.objects.create(
                inscripcion=self.inscripcion,
                tipo_pago=tipo_pago,
                monto=costos['mensualidad'],
                periodo=f"Mes: {mes}",
                numero_pago=mes,
                estado=estado,
                fecha_pago=fecha_pago
            )
            pagos_creados.append(pago)
        return pagos_creados

    def validar_coherencia_conceptos(self, conceptos_ids, monto):
        """Valida que la selección de conceptos sea coherente"""
        # 1. Validar que el monto no sea 0 si hay conceptos seleccionados
        if conceptos_ids and (monto is None or monto == 0):
            return {
                'valido': False,
                'mensaje': 'El monto no puede ser 0 si hay conceptos seleccionados',
                'conceptos_data': None
            }

        # 2. Obtener conceptos de la BD
        conceptos = TipoPago.objects.filter(id__in=conceptos_ids)
        if len(conceptos) != len(conceptos_ids):
            ids_encontrados = set(conceptos.values_list('id', flat=True))
            ids_invalidos = set(conceptos_ids) - ids_encontrados
            return {
                'valido': False,
                'mensaje': f'Los conceptos con IDs {list(ids_invalidos)} no existen',
                'conceptos_data': None
            }

        # 3. Organizar conceptos por tipo
        tiene_inscripcion = False
        tiene_documentacion = False
        tiene_mensualidad = False
        suma_conceptos = 0
        costos = self.obtener_costos_reales()

        conceptos_data = {
            'inscripcion': None,
            'documentacion': None,
            'mensualidades': []
        }

        for concepto in conceptos:
            if concepto.nombre == "Inscripcion":
                tiene_inscripcion = True
                conceptos_data['inscripcion'] = concepto
                suma_conceptos += costos['inscripcion']
            elif concepto.nombre == "Documentacion":
                tiene_documentacion = True
                conceptos_data['documentacion'] = concepto
                suma_conceptos += costos['documentacion']
            elif concepto.nombre == "Mensualidad":
                tiene_mensualidad = True
                conceptos_data['mensualidades'].append(concepto)
                suma_conceptos += costos['mensualidad']

        # 4. REGLA: No se puede pagar SOLO documentación
        if tiene_documentacion and not tiene_inscripcion:
            return {
                'valido': False,
                'mensaje': 'No puedes pagar documentación sin pagar primero la inscripción',
                'conceptos_data': conceptos_data
            }

        # 5. REGLA: No se pueden pagar mensualidades sin inscripción
        if tiene_mensualidad and not tiene_inscripcion:
            return {
                'valido': False,
                'mensaje': 'No puedes pagar mensualidades sin pagar primero la inscripción',
                'conceptos_data': conceptos_data
            }

        # 6. REGLA: El monto debe coincidir con la suma de conceptos
        if abs(suma_conceptos - monto) > 0.01:
            return {
                'valido': False,
                'mensaje': f'El monto (${monto}) no coincide con la suma de conceptos seleccionados (${suma_conceptos})',
                'conceptos_data': conceptos_data
            }

        # 7. TODO CORRECTO
        return {
            'valido': True,
            'mensaje': 'Selección de conceptos válida',
            'conceptos_data': conceptos_data
        }

    def _aplicar_seleccion_manual(self, conceptos_data, notas):
        """Aplica la selección manual de conceptos validada"""
        # Pagar inscripción según selección
        if conceptos_data['inscripcion']:
            self.crear_pago_inscripcion(estado="completado", notas=notas, fecha_pago=timezone.now())
        else:
            self.crear_pago_inscripcion(estado="pendiente", notas=notas)

        # Pagar documentación según selección
        if conceptos_data['documentacion']:
            self.crear_pago_documentacion(estado="completado", notas=notas, fecha_pago=timezone.now())
        else:
            self.crear_pago_documentacion(estado="pendiente", notas=notas)

        # Crear mensualidades según selección
        num_mensualidades_pagadas = len(conceptos_data['mensualidades'])
        tipo_mensualidad = TipoPago.objects.get(nombre="Mensualidad")
        costos = self.obtener_costos_reales()

        for mes in range(1, self.duracion_meses + 1):
            # Las primeras N mensualidades se marcan como completadas
            estado = "completado" if mes <= num_mensualidades_pagadas else "pendiente"
            fecha_pago = timezone.now() if estado == "completado" else None

            Pago.objects.create(
                inscripcion=self.inscripcion,
                tipo_pago=tipo_mensualidad,
                monto=costos['mensualidad'],
                periodo=f"Mes: {mes}",
                numero_pago=mes,
                estado=estado,
                fecha_pago=fecha_pago
            )

        return {
            'success': True,
            'message': 'Pago procesado según selección manual'
        }

    def crear_todos_los_conceptos(self, estado, notas=None, fecha_pago=None):
        """Crea todos los conceptos con el mismo estado"""
        self.crear_pago_inscripcion(estado, notas, fecha_pago)
        self.crear_pago_documentacion(estado, notas, fecha_pago)
        self.crear_pagos_mensualidades(estado, fecha_pago)

    @transaction.atomic
    def procesar_pago_inicial(self, monto, notas=None, conceptos_ids=None):
        """
        Procesa el pago inicial según el monto y conceptos seleccionados.

        Args:
            monto: cantidad a pagar
            notas: observaciones del pago
            conceptos_ids: array de IDs de conceptos seleccionados (opcional)
        """

        # CASO 1: Usuario envió selección manual de conceptos
        if conceptos_ids and len(conceptos_ids) > 0:
            validacion = self.validar_coherencia_conceptos(conceptos_ids, monto)

            if not validacion['valido']:
                return {
                    'success': False,
                    'message': validacion['mensaje']
                }

            # Aplicar selección manual
            return self._aplicar_seleccion_manual(validacion['conceptos_data'], notas)

        # CASO 2: Modo automático - Monto = 0 → Todo pendiente
        if monto is None or monto == 0:
            self.crear_todos_los_conceptos(estado="pendiente", notas=notas)
            return {
                "success": True,
                "message": "Inscripción creada. Todos los pagos están pendientes."
            }

        # CASO 3: Modo automático - Monto >= Total → Todo completado
        total_diplomado = self.calcular_total_diplomado()

        if monto >= total_diplomado:
            self.crear_todos_los_conceptos(estado="completado", notas=notas, fecha_pago=timezone.now())

            if monto > total_diplomado:
                excedente = monto - total_diplomado
                return {
                    "success": False,
                    "message": f"El monto excede el total en ${excedente:.2f}. No se permite sobrepago en esta configuración.",
                    "excedente": excedente
                }

            return {
                "success": True,
                "message": "Inscripción completada. Todos los pagos están cubiertos."
            }

        # CASO 4: Pago parcial sin selección manual → Distribución automática
        return self._distribuir_pago_automatico(monto, notas)

    def _distribuir_pago_automatico(self, monto, notas):
        """Distribuye el pago automáticamente según prioridades"""
        costos = self.obtener_costos_reales()
        monto_restante = monto

        # 1. Validar que alcance al menos para inscripción
        if monto_restante < costos['inscripcion']:
            return {
                'success': False,
                'message': f"Monto insuficiente. Mínimo debe cubrir la inscripción (${costos['inscripcion']:.2f})"
            }

        # 2. Pagar inscripción
        self.crear_pago_inscripcion(estado="completado", notas=notas, fecha_pago=timezone.now())
        monto_restante -= costos['inscripcion']

        # 3. Pagar mensualidades en orden cronológico
        tipo_mensualidad = TipoPago.objects.get(nombre="Mensualidad")
        mensualidades_pagadas = 0

        for mes in range(1, self.duracion_meses + 1):
            if monto_restante >= costos['mensualidad']:
                Pago.objects.create(
                    inscripcion=self.inscripcion,
                    tipo_pago=tipo_mensualidad,
                    monto=costos['mensualidad'],
                    periodo=f"Mes: {mes}",
                    numero_pago=mes,
                    estado="completado",
                    fecha_pago=timezone.now()
                )
                monto_restante -= costos['mensualidad']
                mensualidades_pagadas += 1
            else:
                Pago.objects.create(
                    inscripcion=self.inscripcion,
                    tipo_pago=tipo_mensualidad,
                    monto=costos['mensualidad'],
                    periodo=f"Mes: {mes}",
                    numero_pago=mes,
                    estado="pendiente"
                )

        # 4. Mensaje de resultado
        mensaje = f"Pago parcial procesado: Inscripción pagada"
        if monto_restante > 0:
            mensaje += f", {mensualidades_pagadas} mensualidades pagadas. Saldo restante: ${monto_restante:.2f}"

        return {
            'success': True,
            'message': mensaje,
            'saldo_restante': monto_restante if monto_restante > 0 else 0
        }

    def aplicar_pago(data, user):
        for d in data:
            # 1. Verificar que el pago existe y está pendiente
            pay_qs = Pago.objects.filter(pk=d['id'], estado="pendiente")
            if not pay_qs.exists():
                return {"success": False, "message": "Pago no encontrado o ya completado"}

            pay = pay_qs.first()
            inscripcion = pay.inscripcion
            tipo_pago_nombre = pay.tipo_pago.nombre  # "Inscripcion", "Documentacion", "Mensualidad"

            # 2. VALIDACIÓN: Si es DOCUMENTACIÓN → verificar que inscripción esté pagada
            if tipo_pago_nombre == "Documentacion":
                inscripcion_pagada = Pago.objects.filter(
                    inscripcion=inscripcion,
                    tipo_pago__nombre="Inscripcion",
                    estado="completado"
                ).exists()

                if not inscripcion_pagada:
                    return {
                        "success": False,
                        "message": "No se puede pagar documentación sin haber pagado la inscripción"
                    }

            # 3. VALIDACIÓN: Si es MENSUALIDAD → verificar que inscripción esté pagada
            if tipo_pago_nombre == "Mensualidad":
                inscripcion_pagada = Pago.objects.filter(
                    inscripcion=inscripcion,
                    tipo_pago__nombre="Inscripcion",
                    estado="completado"
                ).exists()

                if not inscripcion_pagada:
                    return {
                        "success": False,
                        "message": "No se puede pagar mensualidades sin haber pagado la inscripción"
                    }

                # 3b. VALIDACIÓN: Mensualidades en orden (tu código actual)
                if pay.numero_pago > 1:
                    numero_pago_anterior = pay.numero_pago - 1
                    pago_anterior_existe = Pago.objects.filter(
                        inscripcion=inscripcion,
                        tipo_pago__nombre="Mensualidad",
                        numero_pago=numero_pago_anterior,
                        estado="completado"
                    ).exists()

                    if not pago_anterior_existe:
                        return {
                            "success": False,
                            "message": f"No se puede pagar la mensualidad {pay.numero_pago} sin haber pagado la mensualidad {numero_pago_anterior}"
                        }

            # 4. Si es INSCRIPCIÓN, no hay validaciones previas (es el primer pago)

            # 5. Si todas las validaciones pasaron, aplicar el pago
            pay.estado = "completado"
            pay.fecha_pago = timezone.now()
            pay.referencia = d.get('referencia')  # ← Guardar la referencia enviada
            pay.modified_by = user
            pay.save()

        # 6. Retornar éxito solo DESPUÉS de procesar TODOS los pagos
        return {
            "success": True,
            "message": "Pago(s) aplicado(s) correctamente"
        }