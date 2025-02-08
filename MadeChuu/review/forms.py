from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review_text', 'review_image']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'class': 'form-control'}),
            'review_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'เขียนความคิดเห็นของคุณที่นี่...'}),
            'review_image': forms.FileInput(attrs={'class': 'form-control'}),  # เพิ่ม widget สำหรับ
        }
        labels = {
            'rating': 'คะแนนรีวิว',
            'review_text': 'ความคิดเห็น',
            'review_image': 'อัปโหลดรูปภาพ',  # เพิ่ม label สำหรับรูปภาพ
        }
