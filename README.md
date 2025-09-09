# 這是我的專案筆記 music_project

## 虛擬環境建置
### 建置虛擬環境
```
python -m venv {虛擬環境名稱}
```
### 啟動虛擬環境（PowerShell）
```
venv\Scripts\Activate.ps1
```
### 安裝 Django
```
pip install django
```
### 確認 Django 安裝成功
```
django-admin --version
```

## 建立專案及APP
### 建立專案
```
django-admin startproject {專案名稱}
```

### 建立 APP
1.進入專案根目錄
```
cd {專案名稱}
```
2.建立 APP：APP 就是專案中的功能模組

```
python manage.py startapp {APP名稱}
```
3.設定settings.py：將APP名稱加入 INSTALLED_APPS
```
INSTALLED_APPS = [
    ...
    '{APP名稱}',
]
```
4.**建立資料庫**
```
python manage.py migrate 
```
5.啟動開發伺服器
```
python manage.py runserver
```
瀏覽器打開 http://127.0.0.1:8000 就可以看到 Django 預設頁面。

### 增加templates及static資料夾：放置各種.html檔案及靜態檔案
*於APP資料夾下新增templates資料夾：放置各種.html檔案  
*於APP資料夾下新增static資料夾，在資料夾內增加四種資料夾 (非必要)，分別為js、plugins、css、images，並設定settings.py
```python
STATIC_URL='/static/'
STATICFILES_DIRS = [BASE_DIR / "static"] # 放在專案根目錄的 static 資料夾
```
** 放在 APP 裡的 static，Django 會自動找到，不一定要寫STATICFILES_DIRS，但放在專案根目錄的話就要設定。 **
### 增加urls.py檔案於APP資料夾下，並設定
```python
from django.urls import path
from django.contrib.auth import views as auth_views # Django 本身就有的 views
from . import views # 自己新增的 views

# 舉例
urlpatterns = [
    path("", views.index, name="index"),
    path("login/", auth_views.LoginView.as_view(), name="login"), # 登入
]
```
<備註> path(url/, view, 別名)  
<補充>login view 自訂模板要加 template_name，否則預設為"registration/login.html"：

```python
path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login")
```
** .as_view() 只用在 class-based views（CBV），function-based views（FBV）不用。**  
** url 最好養成習慣最後要加 "/"，但 Django 會自動 redirect 沒 / 的 URL **


### 專案urls.py 設定
要引入APP的urls.py
``` python
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("music_app.urls")),  # 把 App 的路由加入總路由
]
```

** 建議做法（多 App 專案）**  
-在每個 App 下的 templates 和 static 資料夾中，再建立一個以 App 名稱命名的子資料夾  
-將該 App 的模板與靜態檔案放入這個子資料夾  
-這樣可以避免不同 App 有相同檔名時發生衝突  


----------------------------------------------------------
## 模板的繼承
網站的導覽列及頁尾資訊等共用資訊可以寫在"base.html"供其他模板繼承，可以不必重複寫一樣的東西。  
範例：
```django
<!-- base.html -->
<!DOCTYPE html>
<html>
<head>
    <title>網站標題</title>
</head>
<body>
    <nav>
        <!-- 導覽列 -->
    </nav>

    {% block content %}
    <!-- 子模板的內容會放在這裡 -->
    {% endblock %}

    <footer>
        <!-- 頁尾資訊 -->
    </footer>
</body>
</html>
```

子模板範例：
```django
{% extends "base.html" %}

{% block content %}
<h1>這是子模板的內容</h1>
<p>這部分會被放入 base.html 的 block content 中</p>
{% endblock %}
```
## Django 內建Views (無註冊，要另外寫view)

### 登入、登出、身分驗證
#### Authentication System

| View 類別 | LoginView | LogoutView |
|-----------|-----------|------------|
| **模板 (Template)** | 預設為 `registration/login.html` | 預設為 `registration/logged_out.html` |
| **身分驗證表單 (Form)** | 預設為 `AuthenticationForm` | 不需要表單 |
| **官方說明文件** | [Authentication](https://docs.djangoproject.com/en/5.2/topics/auth/default/) | 同左 |

---

#### Django 內建表單

- `AuthenticationForm`
- `BaseUserCreationForm`
- `PasswordChangeForm`
- `PasswordResetForm`
- `SetPasswordForm`
- `UserChangeForm`
- `UserCreationForm`

### 註冊
```django
class UserRegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "register.html"
    success_url = reverse_lazy("index")
```

### 資料的 CRUD - 新增、更新、刪除
| Views方法 | CreateView | UpdateView | DeleteView |
|-----------|------------|------------|------------|
| **用途** | 用來新增 model 裡的資料 | 用來更新 model 裡的資料 | 用來刪除 model 裡的資料 |
| **參數設定** | ~~1. `model = {model名稱}` → 用來指定 model~~<br>2. `template_name = {.html檔案名稱}` → 用來指定模板（選擇性）<br>3. `fields` 或 `form_class`（二選一，不可同時存在）<br>&nbsp;&nbsp;- `fields = [...]` → Django 會自動產生一個簡單的 ModelForm<br>&nbsp;&nbsp;- `form_class = ...` → 自己定義的 ModelForm<br>4. `success_url = {url別名}` → 操作成功後會到哪 | 同左 | 同左，但注意 **不用填寫 fields 或 form_class** |
| **預設模板名稱** | `<app>/<model>_form.html` | `<app>/<model>_form.html` | `<app>/<model>_confirm_delete.html` |
| **備註** | 1. `template_name`<br>&nbsp;&nbsp;- 對 CreateView / UpdateView，是「表單模板」<br>&nbsp;&nbsp;- 對 DeleteView，是「刪除確認頁模板」<br>2. `fields` / `form_class`<br>&nbsp;&nbsp;- CreateView & UpdateView → 需要設定 fields 或 form_class（二選一）<br>&nbsp;&nbsp;- DeleteView → 不需要，因為只做確認和刪除，不顯示欄位<br>3. `success_url`<br>&nbsp;&nbsp;- CreateView / UpdateView / DeleteView → 都可以設定<br>&nbsp;&nbsp;- 如果 CreateView / UpdateView 沒寫 success_url → Django 會用 `get_absolute_url()` 導向物件<br>&nbsp;&nbsp;- DeleteView 一定要寫 success_url，否則 Django 不知道刪除後去哪裡 | 同左 | 同左 |
| **官方說明文件** | [Django 官方文件](https://docs.djangoproject.com/en/5.2/ref/class-based-views/generic-editing/) | 同左 | 同左 |
| **舉例** |
```python
class UserRegisterView(CreateView):
    model = User
    template_name = "register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("login")
``` 

```python
class PlaylistUpdateView(UpdateView):
    model = Playlist
    template_name = "playlist_update.html"
    form_class = PlaylistForm
    success_url = reverse_lazy("playlist_view")
``` 
```python
class PlaylistDeleteView(DeleteView):
    model = Playlist
    template_name = "playlist_delete.html"
    success_url = reverse_lazy("playlist_view")
```
### 資料的 CRUD - 讀取
| Views方法      | DetailView                           | ListView                              |
|----------------|------------------------------------|--------------------------------------|
| 用途           | 顯示單一物件的詳細資料（Detail）      | 顯示多筆物件列表（List）              |
| 參數設定       | 1. model<br>2. template_name<br>3. context_object_name → 選填，模板中物件的變數名稱（預設為 object）<br>4. pk_url_kwarg / slug_url_kwarg → URL 中取得物件的 pk 或 slug（預設會找 URL 中的 pk ） | 1. model<br>2. template_name<br>3. context_object_name → 模板中列表的變數名稱（預設為 object_list）<br>4. paginate_by → 分頁用，每頁顯示多少筆 |
| 官方說明文件   | [Generic display views](https://docs.djangoproject.com/en/5.2/ref/class-based-views/generic-display/) | 同左 |
| 舉例
```python
class PlaylistDetailView(DetailView):
    model = Playlist
    template_name = "playlist_detail.html"
    context_object_name = "playlist"
# 記得要從 html 傳入 pk
```
```python
class PlaylistView(ListView):
    model = Playlist
    template_name = "playlist.html"
    context_object_name = "playlists"
```

### 資料 CRUD 方法統整
| CRUD | ORM 方法| CBV 方法|
|------|---------|--------|
| Create | `objects.create()`| `CreateView` |
| Read | `objects.get()/filter()/all()`| `DetailView / ListView` |
| Update | 修改物件後 `.save()`| `UpdateView` |
| Delete | `.delete()` | `DeleteView` |

### 表格 - ModelForm & Form
| 類型 | ModelForm | Form |
|------|-----------|------|
| 特性 | 可以直接操作資料庫，資料表有的欄位都可以選 | 一般表格，需要自定義表格的欄位 |
| 是否可以自訂表格欄位 | 可以 | 可以 |
| ORM 支援 | 可以搭配 CreateView、UpdateView、DeleteView | 必須手動在 view 拿資料，再用 ORM 存資料 |
| 用途 | 1. 可以在 template 中利用 `{{ form.as_p }}` 根據表格欄位自動生成表格<br>2. 可搭配原生的新增、刪除、修改方法，直接更改資料庫的資料 | 可以在 template 中利用 `{{ form.as_p }}` 根據表格欄位自動生成表格 |
| 備註 | - 欄位 (CharField, IntegerField, EmailField 等) → 用來定義使用者輸入的資料類型和驗證規則<br>- widget → 控制 HTML 表單外觀（單行、textarea、密碼欄位等）<br>- 要改 HTML 屬性（CSS、placeholder…） → 必須用 widget + attrs<br>- attrs 是 widget 的參數，用來設定 HTML 屬性，attrs 裡可以放 class、placeholder、id、style 等 HTML 屬性<br>- **Python/Django 命名慣例**：欄位名稱建議使用小寫，例如 `username`, `password` | 同左 |
| 參數設定 | class Meta<br>- model = {model名稱} → 用來指定 model<br>- fields = [] → 選擇 model 裡面的欄位 | 自定義欄位 |
| 官方說明文件 | - [Form fields](https://docs.djangoproject.com/en/5.2/ref/forms/fields/)<br>- [Widgets](https://docs.djangoproject.com/en/5.2/ref/forms/widgets/) | 同左 |
| 舉例 | 
```python
from django import forms
from django.contrib.auth.models import User

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='密碼')

    class Meta:
        model = User
        fields = ["username", "email"]
        labels = {"username": "帳號", "email": "電子郵件"}
``` 
```python
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='帳號')
    password = forms.CharField(widget=forms.PasswordInput, label='密碼')
```



## django-crispy-forms 插件
1.安裝：
```
pip install django-crispy-forms
pip install crispy-bootstrap5
```
2.設定(settings.py)：
```python
INSTALLED_APPS = [
    ...
    'crispy_forms',
    'crispy_bootstrap5',
]
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = 'bootstrap5'
```
3.使用方式(template)：用 |crispy 代替 as_p
```html
{% load crispy_forms_tags %}
<form method="post">
    {% csrf_token %}
    {{ form|crispy }}
    <button type="submit" class="btn btn-primary">送出</button>
</form>
```

