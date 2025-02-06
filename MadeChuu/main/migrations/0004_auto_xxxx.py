from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_image',
            field=models.ImageField(upload_to='ProductDetail/static/images', blank=True, null=True),
        ),
    ]