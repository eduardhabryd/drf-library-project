# Generated by Django 4.2.6 on 2023-10-25 18:40

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        (
            "borrowings",
            "0002_alter_borrowing_book_id_alter_borrowing_borrow_date_and_more",
        ),
    ]

    operations = [
        migrations.RenameField(
            model_name="borrowing",
            old_name="book_id",
            new_name="book",
        ),
        migrations.RenameField(
            model_name="borrowing",
            old_name="user_id",
            new_name="user",
        ),
    ]
