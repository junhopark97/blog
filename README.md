# project

## 🛠 Stack
<img src="https://img.shields.io/badge/Python-blue?style=flat-square&logo=python&logoColor=white"/> <img src="https://img.shields.io/badge/Django-0C3C26?style=flat-square&logo=django&logoColor=white"/> <img src="https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=MySQL&logoColor=white"/> <img src="https://img.shields.io/badge/DRF-red?style=flat-square&logo=django&logoColor=white"/> <img src="https://img.shields.io/badge/pytest-0A9EDC?style=flat-square&logo=pytest&logoColor=white"/> <img src="https://img.shields.io/badge/simple_jwt-black?style=flat-square&logo=JSON Web Tokens&logoColor=white"/>

## 📚 API Document
### 👤 USER
| 기능                                                                                                                                   |Http Method| API          |
|--------------------------------------------------------------------------------------------------------------------------------------|---|--------------|
| [회원가입](https://github.com/junhopark97/project/blob/447ec70c84b6d691787d9fc55c3343557541db5b/accounts/serializers.py#L19)             |POST| /api/register/ |
| [로그인](https://github.com/junhopark97/project/blob/447ec70c84b6d691787d9fc55c3343557541db5b/accounts/views.py#L17)                    |POST| /api/login/    |
| [로그아웃](https://github.com/junhopark97/project/blob/447ec70c84b6d691787d9fc55c3343557541db5b/accounts/views.py#L69)                   |POST| /api/logout/   |
| [JWT 유효성 검증 및 갱신](https://github.com/junhopark97/project/blob/447ec70c84b6d691787d9fc55c3343557541db5b/accounts/serializers.py#L100) |GET| /api/verify/   |

<br />

### 🗒 BLOG_POST
| 기능 |Http Method| API |
|-----|---|------|
| 게시물 생성 |POST| /posts/ |
| 게시물 목록 조회 |GET| /posts/ |
| 게시물 id 조회 |GET| /posts/<post_id>/ |
| 게시물 수정 |PUT| /posts/<post_id>/ |
| 게시물 삭제 |DELETE| /posts/<post_id>/ |

<br />

### 📝 COMMENT
| 기능 |Http Method| API |
|-----|---|------|
| 댓글 생성 |POST| /comments/ |
| 댓글 삭제 |PUT| /comments/ |
| 댓글 삭제 |DELETE| /comments/ |

<br />

### 👍 LIKE_POST
| 기능 |Http Method| API |
|-----|---|------|
| 게시물 좋아요 |POST| /posts/like/<post_id>/ |


<br />

<hr/>

#### 회원가입 - /account/register/
<pre>
- request -

body = {
    "email": "test@test.com",
    "password": "test1234!",
    "password2": "test1234!",
    "gender": "M",
    "username":"test",
    "phone_number": "01000000000"
}
</pre>

<pre>
- response -

data = {
    "email": "test@test.com",
    "gender": "M",
    "username": "test",
    "phone_number": "01000000000",
    "token": {
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90JpYXQiOjE2ODEzNjcxOD]5MWUyYjU5M2Y4MjYzYzZjIiwidXNlcl9pZCI6IjUiLCJlbWFpbCI6InRlc3Q0QHRlc3QuY29tIn0.obumny21TkFgUZubsZ8zIhRqXnii5lH4grwTI1zK2FY",
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90zUUxNjM1YjE0NDI3ODI5M2RiMTFlMTBkMmIyNyIsInVzZXJfaWQiOiI1IiwiZW1haWwiOiJ0ZXN0NEB0ZXN0LmNvbSJ9.lI2b53ojDG1D4nc0jFtwkg1myYIM12UHv7H9enNh0U8"
    }
}
</pre>

#### 로그인 - /account/login/
<pre>
- request -

body = {
    "email" = "test@test.com",
    "password" = "password1234!"
}
</pre>
<pre>
- response -

data = {
    "token": {
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90JpYXQiOjE2ODEzNjcxOD]5MWUyYjU5M2Y4MjYzYzZjIiwidXNlcl9pZCI6IjUiLCJlbWFpbCI6InRlc3Q0QHRlc3QuY29tIn0.obumny21TkFgUZubsZ8zIhRqXnii5lH4grwTI1zK2FY",
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90zUUxNjM1YjE0NDI3ODI5M2RiMTFlMTBkMmIyNyIsInVzZXJfaWQiOiI1IiwiZW1haWwiOiJ0ZXN0NEB0ZXN0LmNvbSJ9.lI2b53ojDG1D4nc0jFtwkg1myYIM12UHv7H9enNh0U8"
    },
    "message": "Login success"
}
</pre>

#### 로그아웃 - /account/logout/
<pre>
- request -

cookie['jwt'] = {
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90JpYXQiOjE2ODEzNjcxOD]5MWUyYjU5M2Y4MjYzYzZjIiwidXNlcl9pZCI6IjUiLCJlbWFpbCI6InRlc3Q0QHRlc3QuY29tIn0.obumny21TkFgUZubsZ8zIhRqXnii5lH4grwTI1zK2FY",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90zUUxNjM1YjE0NDI3ODI5M2RiMTFlMTBkMmIyNyIsInVzZXJfaWQiOiI1IiwiZW1haWwiOiJ0ZXN0NEB0ZXN0LmNvbSJ9.lI2b53ojDG1D4nc0jFtwkg1myYIM12UHv7H9enNh0U8"
},
</pre>
<pre>
- response -

data = {
    "message": "Logout Successful",
}
</pre>
