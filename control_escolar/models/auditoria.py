from django.db import models
from common.models import Base, OwnerBaseModel

class ModuloComplete(Base, OwnerBaseModel):
    user = models.ForeignKey("user.UserCustomize", on_delete=models.CASCADE, related_name="student_progress")
    programa = models.ForeignKey("control_escolar.ProgramaEducativo", on_delete=models.CASCADE, related_name="program_progress")
    modulo = models.ForeignKey("control_escolar.ModuloEducativo", on_delete=models.CASCADE, related_name="modulo_progress")
    submodulo = models.ForeignKey("control_escolar.SubModuloEducativo", on_delete=models.CASCADE, related_name="submodulo_progress", null=True, blank=True)
    completed = models.BooleanField(default=False)
    pocentaje_progreso = models.DecimalField(decimal_places=2, default=0)
    date_completed = models.DateField(null=True, blank=True)
    
class TimeSession(Base, OwnerBaseModel):
    user = models.ForeignKey("user.UserCustomize", on_delete=models.CASCADE, related_name="student_session")
    programa = models.ForeignKey("control_escolar.ProgramaEducativo", on_delete=models.CASCADE, related_name="program_session")
    modulo = models.ForeignKey("control_escolar.ModuloEducativo", on_delete=models.CASCADE, related_name="modulo_session")
    date_start = models.DateField(auto_now_add=True)
    date_finish = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    @property
    def duration_minutes(self):
        if self.date_finish:
            delta = self.date_finish - self.date_start
            return delta.total_seconds() / 60
        
        return None