from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("suppliers", "0001_initial"),
        ("users", "0002_shoppermission"),
    ]

    operations = [
        migrations.AddField(
            model_name="employeeprofile",
            name="suppliers",
            field=models.ManyToManyField(
                blank=True,
                related_name="employees",
                to="suppliers.supplier",
                verbose_name="working suppliers",
            ),
        ),
    ]

