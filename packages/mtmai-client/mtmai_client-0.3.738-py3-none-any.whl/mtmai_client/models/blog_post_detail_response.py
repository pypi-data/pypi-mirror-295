from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="BlogPostDetailResponse")


@_attrs_define
class BlogPostDetailResponse:
    """
    Attributes:
        id (str):
        title (str):
        content (str):
        tags (List[str]):
        author_id (Union[None, str]):
        author_avatar (Union[None, str]):
        author_email (Union[None, str]):
        author_website (Union[None, str]):
        author_bio (Union[None, str]):
        author_location (Union[None, str]):
        author_company (Union[None, str]):
        author_job_title (Union[None, str]):
        author_skills (Union[List[str], None]):
        author_interests (Union[List[str], None]):
        author_hobbies (Union[List[str], None]):
        author_languages (Union[List[str], None]):
        author_languages_level (Union[List[str], None]):
    """

    id: str
    title: str
    content: str
    tags: List[str]
    author_id: Union[None, str]
    author_avatar: Union[None, str]
    author_email: Union[None, str]
    author_website: Union[None, str]
    author_bio: Union[None, str]
    author_location: Union[None, str]
    author_company: Union[None, str]
    author_job_title: Union[None, str]
    author_skills: Union[List[str], None]
    author_interests: Union[List[str], None]
    author_hobbies: Union[List[str], None]
    author_languages: Union[List[str], None]
    author_languages_level: Union[List[str], None]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        title = self.title

        content = self.content

        tags = self.tags

        author_id: Union[None, str]
        author_id = self.author_id

        author_avatar: Union[None, str]
        author_avatar = self.author_avatar

        author_email: Union[None, str]
        author_email = self.author_email

        author_website: Union[None, str]
        author_website = self.author_website

        author_bio: Union[None, str]
        author_bio = self.author_bio

        author_location: Union[None, str]
        author_location = self.author_location

        author_company: Union[None, str]
        author_company = self.author_company

        author_job_title: Union[None, str]
        author_job_title = self.author_job_title

        author_skills: Union[List[str], None]
        if isinstance(self.author_skills, list):
            author_skills = self.author_skills

        else:
            author_skills = self.author_skills

        author_interests: Union[List[str], None]
        if isinstance(self.author_interests, list):
            author_interests = self.author_interests

        else:
            author_interests = self.author_interests

        author_hobbies: Union[List[str], None]
        if isinstance(self.author_hobbies, list):
            author_hobbies = self.author_hobbies

        else:
            author_hobbies = self.author_hobbies

        author_languages: Union[List[str], None]
        if isinstance(self.author_languages, list):
            author_languages = self.author_languages

        else:
            author_languages = self.author_languages

        author_languages_level: Union[List[str], None]
        if isinstance(self.author_languages_level, list):
            author_languages_level = self.author_languages_level

        else:
            author_languages_level = self.author_languages_level

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "title": title,
                "content": content,
                "tags": tags,
                "author_id": author_id,
                "author_avatar": author_avatar,
                "author_email": author_email,
                "author_website": author_website,
                "author_bio": author_bio,
                "author_location": author_location,
                "author_company": author_company,
                "author_job_title": author_job_title,
                "author_skills": author_skills,
                "author_interests": author_interests,
                "author_hobbies": author_hobbies,
                "author_languages": author_languages,
                "author_languages_level": author_languages_level,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        title = d.pop("title")

        content = d.pop("content")

        tags = cast(List[str], d.pop("tags"))

        def _parse_author_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        author_id = _parse_author_id(d.pop("author_id"))

        def _parse_author_avatar(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        author_avatar = _parse_author_avatar(d.pop("author_avatar"))

        def _parse_author_email(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        author_email = _parse_author_email(d.pop("author_email"))

        def _parse_author_website(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        author_website = _parse_author_website(d.pop("author_website"))

        def _parse_author_bio(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        author_bio = _parse_author_bio(d.pop("author_bio"))

        def _parse_author_location(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        author_location = _parse_author_location(d.pop("author_location"))

        def _parse_author_company(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        author_company = _parse_author_company(d.pop("author_company"))

        def _parse_author_job_title(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        author_job_title = _parse_author_job_title(d.pop("author_job_title"))

        def _parse_author_skills(data: object) -> Union[List[str], None]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                author_skills_type_0 = cast(List[str], data)

                return author_skills_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List[str], None], data)

        author_skills = _parse_author_skills(d.pop("author_skills"))

        def _parse_author_interests(data: object) -> Union[List[str], None]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                author_interests_type_0 = cast(List[str], data)

                return author_interests_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List[str], None], data)

        author_interests = _parse_author_interests(d.pop("author_interests"))

        def _parse_author_hobbies(data: object) -> Union[List[str], None]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                author_hobbies_type_0 = cast(List[str], data)

                return author_hobbies_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List[str], None], data)

        author_hobbies = _parse_author_hobbies(d.pop("author_hobbies"))

        def _parse_author_languages(data: object) -> Union[List[str], None]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                author_languages_type_0 = cast(List[str], data)

                return author_languages_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List[str], None], data)

        author_languages = _parse_author_languages(d.pop("author_languages"))

        def _parse_author_languages_level(data: object) -> Union[List[str], None]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                author_languages_level_type_0 = cast(List[str], data)

                return author_languages_level_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List[str], None], data)

        author_languages_level = _parse_author_languages_level(d.pop("author_languages_level"))

        blog_post_detail_response = cls(
            id=id,
            title=title,
            content=content,
            tags=tags,
            author_id=author_id,
            author_avatar=author_avatar,
            author_email=author_email,
            author_website=author_website,
            author_bio=author_bio,
            author_location=author_location,
            author_company=author_company,
            author_job_title=author_job_title,
            author_skills=author_skills,
            author_interests=author_interests,
            author_hobbies=author_hobbies,
            author_languages=author_languages,
            author_languages_level=author_languages_level,
        )

        blog_post_detail_response.additional_properties = d
        return blog_post_detail_response

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
