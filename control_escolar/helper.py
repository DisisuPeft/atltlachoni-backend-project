from django.db.models.aggregates import Max
from django.utils import timezone
from user.models import EstudiantePerfil

def generate_matricula():
    year = timezone.now().year
    estudiantes_max_year = EstudiantePerfil.objects.filter(fecha_ingreso__year=year).aggregate(Max('matricula'))
    # print(estudiantes_max_year)
    flag = 0
    if estudiantes_max_year['matricula__max'] is None:
        secuencial = str(flag+1).zfill(6)
        return f"{year}{secuencial}"
    else:
        matricula_max = estudiantes_max_year['matricula__max']
        nueva_matricula = int(matricula_max[4:])

        secuencial = str(nueva_matricula + 1).zfill(6)

        return f"{year}{secuencial}"
