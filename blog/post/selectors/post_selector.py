from post.models import Post
from user.models import User


class Paginator:
    def __init__(self, page_size: int) -> None:
        self.page_size = page_size

    def calc_start_end(self, page_num: int):
        if page_num <= 0:
            raise ValueError("page num is > 0")

        start = (page_num - 1) * self.page_size
        end = start + self.page_size
        return start, end


def get_following_post_by_page(user_id: int, page_num: int):
    user = User.objects.get(id=user_id)
    follows = user.follows.all()
    posts = Post.objects.filter(author_id__in=follows).values("id", "title", "content")

    paginator: Paginator = Paginator(5)
    start, end = paginator.calc_start_end(page_num)
    page_posts = posts[
        start:end
    ]  # orm에서 슬라이싱을 적절하게 처리 limit와 Offset으로 진행

    if not len(page_posts):
        data = {"msg": "Empty posts"}
    else:
        data = {"posts": list(page_posts)}
    return data
