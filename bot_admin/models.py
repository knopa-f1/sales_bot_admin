from django.db import models


class Catalog(models.Model):
    name = models.CharField("Название", max_length=255)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='subcategories',
        on_delete=models.CASCADE,
        verbose_name="Родитель"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return f"{self.parent.name} / {self.name}" if self.parent else self.name


class Product(models.Model):
    catalog = models.ForeignKey(
        Catalog,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name="Категория"
    )
    name = models.CharField("Название", max_length=255)
    description = models.TextField("Описание", blank=True)
    image = models.ImageField("Изображение", upload_to='product_images/')
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name


class User(models.Model):
    chat_id = models.BigIntegerField("Telegram chat ID", unique=True)
    name = models.CharField("Имя", max_length=255)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.name} ({self.chat_id})"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items', verbose_name="Пользователь")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    count = models.PositiveIntegerField("Количество", default=1)

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"

    def __str__(self):
        return f"{self.user.name} - {self.product.name} x{self.count}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name="Пользователь")
    amount = models.DecimalField("Сумма", max_digits=10, decimal_places=2)
    address = models.TextField("Адрес доставки")
    transaction_id = models.CharField("ID транзакции", max_length=255)
    status = models.CharField("Статус", max_length=50, default='unpaid')

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ #{self.id} — {self.user.name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    count = models.PositiveIntegerField("Количество")
    amount = models.DecimalField("Сумма", max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Товар в заказе"
        verbose_name_plural = "Товары в заказе"

    def __str__(self):
        return f"{self.order.id} - {self.product.name} x{self.count}"


class Broadcast(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('sent', 'Отправлено'),
        ('error', 'Ошибка'),
    ]

    message = models.TextField("Текст сообщения")
    recipients = models.ManyToManyField(User, verbose_name="Получатели")
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    sent_at = models.DateTimeField("Отправлено", null=True, blank=True)

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"

    def __str__(self):
        return f"Рассылка #{self.id} ({self.status})"
