# Generated manually for RBAC

from django.db import migrations, models


def assign_group_permissions(apps, schema_editor) -> None:
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    ContentType = apps.get_model("contenttypes", "ContentType")

    db_alias = schema_editor.connection.alias
    ct, _ = ContentType.objects.using(db_alias).get_or_create(
        app_label="users",
        model="shoppermission",
    )

    perm_definitions = [
        ("place_order", "Place orders as customer"),
        ("view_own_orders", "View own customer orders"),
        ("view_active_promotions", "View active promotional codes"),
        ("submit_product_review", "Submit product reviews"),
        ("view_suppliers", "View supplier directory"),
        ("view_sales", "View sales information"),
        ("manage_products", "Manage catalog products"),
        ("full_access", "Full administrative access to shop APIs"),
    ]
    for codename, name in perm_definitions:
        Permission.objects.using(db_alias).get_or_create(
            content_type=ct,
            codename=codename,
            defaults={"name": name},
        )

    perms = {p.codename: p for p in Permission.objects.using(db_alias).filter(content_type=ct)}

    def pick(*codes: str) -> list:
        return [perms[c] for c in codes if c in perms]

    customer, _ = Group.objects.using(db_alias).get_or_create(name="customer")
    customer.permissions.set(
        pick(
            "place_order",
            "view_own_orders",
            "view_active_promotions",
            "submit_product_review",
        ),
    )

    employee, _ = Group.objects.using(db_alias).get_or_create(name="employee")
    employee.permissions.set(
        pick(
            "view_suppliers",
            "view_sales",
            "manage_products",
        ),
    )

    admin_group, _ = Group.objects.using(db_alias).get_or_create(name="admin")
    admin_group.permissions.set(list(Permission.objects.using(db_alias).filter(content_type=ct)))


def noop_reverse(apps, schema_editor) -> None:
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
        ("auth", "0012_alter_user_first_name_max_length"),
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="ShopPermission",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
            options={
                "default_permissions": (),
                "permissions": [
                    ("place_order", "Place orders as customer"),
                    ("view_own_orders", "View own customer orders"),
                    ("view_active_promotions", "View active promotional codes"),
                    ("submit_product_review", "Submit product reviews"),
                    ("view_suppliers", "View supplier directory"),
                    ("view_sales", "View sales information"),
                    ("manage_products", "Manage catalog products"),
                    ("full_access", "Full administrative access to shop APIs"),
                ],
            },
        ),
        migrations.RunPython(assign_group_permissions, noop_reverse),
    ]
