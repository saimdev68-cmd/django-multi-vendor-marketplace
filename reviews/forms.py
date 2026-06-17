from django import forms
from .models import Review


class ProductReviewForm(forms.ModelForm):
    """
    Data collection gate for capturing verified customer product reviews.
    Transforms the positive integer rating field into a readable dropdown selection.
    """
    rating = forms.ChoiceField(
        choices=[
            ("", "Choose a rating..."),
            ("5", "5 Stars ★★★★★ (Excellent)"),
            ("4", "4 Stars ★★★★☆ (Good)"),
            ("3", "3 Stars ★★★☆☆ (Average)"),
            ("2", "2 Stars ★★☆☆☆ (Poor)"),
            ("1", "1 Star  ★☆☆☆☆ (Terrible)"),
        ],
        widget=forms.Select(attrs={
            "class": "form-control review-select-dropdown",
            "style": "width: 100%; padding: 10px; border-radius: 6px; border: 1px solid #ccc; font-size: 1rem;"
        }),
        label="Your Rating"
    )
    
    comment = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            "placeholder": "Share your honest experience with this product... What did you like or dislike?",
            "class": "form-control review-textarea-input",
            "rows": 5,
            "style": "width: 100%; padding: 12px; border-radius: 6px; border: 1px solid #ccc; font-size: 1rem; resize: vertical;"
        }),
        label="Written Commentary"
    )

    class Meta:
        model = Review
        fields = ["rating", "comment"]

    def clean_rating(self):
        """Converts the choice string back to an integer safe for model validation fields."""
        raw_rating = self.cleaned_data.get("rating")
        try:
            return int(raw_rating)
        except (ValueError, TypeError):
            raise forms.ValidationError("Please select a valid numerical rating option.")