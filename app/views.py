from django.http import HttpResponse

def index(request):
    return HttpResponse("""
        <h2>Это административный интерфейс</h2>
        <p>Перейдите по <a href="/admin/">ссылке</a> для работы с системой управления.</p>
    """)
