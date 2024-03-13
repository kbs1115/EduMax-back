from rest_framework.exceptions import ValidationError

from community.domain.definition import TREE_STRUCTURE


class CategoryValidator:
    @classmethod
    def is_valid_hierarchy(cls, category, subcategory):
        if category in TREE_STRUCTURE and subcategory in TREE_STRUCTURE[category]:
            return True
        return False

    @classmethod
    def validate(cls, data):
        if data["category_d4"] and not data["category_d3"]:
            raise ValidationError("Category Depth 4 requires Category Depth 3")
        if data["category_d3"] and not data["category_d2"]:
            raise ValidationError("Category Depth 3 requires Category Depth 2")
        if data["category_d2"] and not data["category_d1"]:
            raise ValidationError("Category Depth 2 requires Category Depth 1")

        if data["category_d4"] and not CategoryValidator.is_valid_hierarchy(
                data["category_d3"], data["category_d4"]
        ):
            raise ValidationError(
                "category depth 4 cannot exist without category depth 3"
            )
        if data["category_d3"] and not CategoryValidator.is_valid_hierarchy(
                data["category_d2"], data["category_d3"]
        ):
            raise ValidationError(
                "category depth 3 cannot exist without category depth 2"
            )
        if data["category_d2"] and not CategoryValidator.is_valid_hierarchy(
                data["category_d1"], data["category_d2"]
        ):
            raise ValidationError(
                "category depth 2 cannot exist without category depth 1"
            )


class LikeValidator:
    @classmethod
    def validate(cls, obj):
        if obj.post and obj.comment:
            raise ValidationError("Like is only for either post or comment type.")
