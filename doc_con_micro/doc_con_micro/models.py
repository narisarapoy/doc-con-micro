from django.db import models

class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name_en = models.TextField()
    name_th = models.TextField()

    def __str__(self):
        return self.id

class RequestDocument(models.Model):
    id = models.AutoField(primary_key=True)
    submit_date = models.TextField()
    department_id = models.TextField()
    telephone = models.TextField()
    req_type = models.IntegerField(default=0)
    req_new = models.TextField()
    req_cancel = models.TextField()
    req_doctype_control = models.TextField()
    req_doctype_uncontrol = models.TextField()
    req_alter = models.TextField()
    req_other = models.TextField()
    req_user_id = models.TextField()
    approved_name = models.TextField()
    response_code = models.TextField()
    master_list_cancel = models.BooleanField(default=False)
    master_list_edit = models.BooleanField(default=False)
    response_other = models.TextField()
    response_name = models.TextField()
    response_date = models.TextField()
    response_original_number = models.BooleanField(default=False)
    request_name = models.TextField()
    request_position = models.TextField(default="")
    request_date = models.TextField()
    control_receive_complete_file = models.BooleanField(default=False)
    control_keep_original_and_restore_copy = models.BooleanField(default=False)
    control_destroy_copy = models.BooleanField(default=False)
    control_send_copy = models.BooleanField(default=False)
    control_name = models.TextField()
    control_date = models.TextField()
    has_attached_doc = models.BooleanField(default=False)
    approved = models.BooleanField(null=True)
    control_type = models.IntegerField(default=0)
    response_type = models.IntegerField(default=0)
    department = models.TextField(default="")
    progress = models.IntegerField(default=0)
    receive_name = models.TextField(default="")
    receive_date = models.TextField(default="")
    request_number_in_year = models.TextField(null=True)
    year = models.TextField(null=True)

    def __str__(self):
        return self.id
