from app.utils.enums import Roles
from app.schemas.citas import AdminCitaFiltersSchema, DoctorAppointmentFiltersSchema, SecretariaAppointmentFiltersSchema
    
schema_by_role = {
    Roles.ADMIN.value : AdminCitaFiltersSchema,
    Roles.SECRETARIA.value : SecretariaAppointmentFiltersSchema,
    Roles.DOCTOR.value : DoctorAppointmentFiltersSchema
}