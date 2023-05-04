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
