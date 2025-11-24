from django import forms
from .models import StudentProfile, Department, Major, Course, Enrollment

class StudentProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 为department字段添加空选项
        self.fields['department'].empty_label = "请选择院系"
        self.fields['major'].empty_label = "请选择专业"

        # 如果是编辑模式且有已选择的院系，则过滤专业选项
        if self.instance and self.instance.pk and self.instance.department:
            self.fields['major'].queryset = Major.objects.filter(department=self.instance.department)
        else:
            self.fields['major'].queryset = Major.objects.none()
            self.fields['major'].disabled = True

    class Meta:
        model = StudentProfile
        fields = ['student_id', 'real_name', 'gender', 'birth_date',
                 'department', 'major', 'address', 'emergency_contact', 'emergency_phone']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'major': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'student_id': '学号',
            'real_name': '真实姓名',
            'gender': '性别',
            'birth_date': '出生日期',
            'department': '所属院系',
            'major': '专业',
            'address': '家庭住址',
            'emergency_contact': '紧急联系人',
            'emergency_phone': '紧急联系电话',
        }

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'code', 'description', 'head_name', 'phone']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'name': '院系名称',
            'code': '院系代码',
            'description': '院系描述',
            'head_name': '院系负责人',
            'phone': '联系电话',
        }

class MajorForm(forms.ModelForm):
    class Meta:
        model = Major
        fields = ['department', 'name', 'code', 'duration', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'department': '所属院系',
            'name': '专业名称',
            'code': '专业代码',
            'duration': '学制(年)',
            'description': '专业描述',
        }

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code', 'course_type', 'credits', 'hours', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'name': '课程名称',
            'code': '课程代码',
            'course_type': '课程类型',
            'credits': '学分',
            'hours': '学时',
            'description': '课程描述',
        }

class EnrollmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 为字段添加Bootstrap样式
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        # 设置学期选项
        semester_choices = [
            ('', '请选择学期'),
            ('第1学期', '第1学期（大一上）'),
            ('第2学期', '第2学期（大一下）'),
            ('第3学期', '第3学期（大二上）'),
            ('第4学期', '第4学期（大二下）'),
            ('第5学期', '第5学期（大三上）'),
            ('第6学期', '第6学期（大三下）'),
            ('第7学期', '第7学期（大四上）'),
            ('第8学期', '第8学期（大四下）'),
        ]
        self.fields['semester'] = forms.ChoiceField(
            choices=semester_choices,
            widget=forms.Select(attrs={'class': 'form-select'}),
            label='学期'
        )

        # 设置学年选项
        import datetime
        current_year = datetime.datetime.now().year
        academic_years = []
        for year in range(current_year - 3, current_year + 3):
            academic_year = f"{year}-{year + 1}"
            academic_years.append((academic_year, f"{academic_year}学年"))

        academic_year_choices = [('', '请选择学年')] + academic_years
        self.fields['academic_year'] = forms.ChoiceField(
            choices=academic_year_choices,
            widget=forms.Select(attrs={'class': 'form-select'}),
            label='学年'
        )

    class Meta:
        model = Enrollment
        fields = ['student', 'course']  # 排除major、semester和academic_year字段，因为我们在__init__中动态定义它们


class AdminEnrollmentForm(forms.ModelForm):
    """管理员专用选课表单，包含专业字段"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 为字段添加Bootstrap样式
        self.fields['student'].widget.attrs.update({'class': 'form-select'})
        self.fields['course'].widget.attrs.update({'class': 'form-select'})
        self.fields['major'].widget.attrs.update({'class': 'form-select'})

        # 设置学期选项
        semester_choices = [
            ('', '请选择学期'),
            ('第1学期', '第1学期（大一上）'),
            ('第2学期', '第2学期（大一下）'),
            ('第3学期', '第3学期（大二上）'),
            ('第4学期', '第4学期（大二下）'),
            ('第5学期', '第5学期（大三上）'),
            ('第6学期', '第6学期（大三下）'),
            ('第7学期', '第7学期（大四上）'),
            ('第8学期', '第8学期（大四下）'),
        ]
        self.fields['semester'] = forms.ChoiceField(
            choices=semester_choices,
            widget=forms.Select(attrs={'class': 'form-select'}),
            label='学期'
        )

        # 设置学年选项
        import datetime
        current_year = datetime.datetime.now().year
        academic_years = []
        for year in range(current_year - 3, current_year + 3):
            academic_year = f"{year}-{year + 1}"
            academic_years.append((academic_year, f"{academic_year}学年"))

        academic_year_choices = [('', '请选择学年')] + academic_years
        self.fields['academic_year'] = forms.ChoiceField(
            choices=academic_year_choices,
            widget=forms.Select(attrs={'class': 'form-select'}),
            label='学年'
        )

    class Meta:
        model = Enrollment
        fields = ['student', 'course', 'major']  # 包含major字段，semester和academic_year在__init__中动态定义
        widgets = {
            'student': forms.Select(attrs={'class': 'form-select'}),
            'course': forms.Select(attrs={'class': 'form-select'}),
            'major': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'student': '学生',
            'course': '课程',
            'major': '专业',
        }

class GradeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 为字段添加Bootstrap样式
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Enrollment
        fields = ['grade', 'score']
        widgets = {
            'grade': forms.Select(attrs={'class': 'form-select'}),
            'score': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100, 'step': 0.5}),
        }
        labels = {
            'grade': '成绩等级',
            'score': '分数',
        }