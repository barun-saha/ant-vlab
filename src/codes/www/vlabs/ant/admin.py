from .models import *
from django.contrib import admin

class TheoryAdmin(admin.ModelAdmin):
    model = Theory
    ordering = ('id',)

class SimulationAdmin(admin.ModelAdmin):
    model = Simulation
    ordering = ('theory',)

class SelfEvaluationAdmin(admin.ModelAdmin):
    model = SelfEvaluation
    ordering = ('theory', 'question_num',)

class SolutionAdmin(admin.ModelAdmin):
    model = Solution
    ordering = ('exercise',)

class ReferenceAdmin(admin.ModelAdmin):
    model = Reference
    ordering = ('theory',)

class ExerciseAdmin(admin.ModelAdmin):
    model = Exercise
    ordering = ('theory', 'problem_id',)

class DefaultCodeAdmin(admin.ModelAdmin):
    model = DefaultCode
    ordering = ('exercise', 'code_type', 'code')
    
#class ChoiceInline(admin.TabularInline):
#        model = Choice
#        extra = 3
#
#class PollAdmin(admin.ModelAdmin):
#        # For display screen
#        list_display = ('question', 'pub_date', 'wasPublishedToday')
#        list_filter  = ['pub_date',]
#        search_fields= ['question',]
#
#        # For add / edit screen
#        fields = ['pub_date', 'question']
#        inlines = [ChoiceInline]

class DefaultCodeAdmin(admin.ModelAdmin):
    model = DefaultCode
    ordering = ('exercise', 'code_type', 'code')


admin.site.register(Theory, TheoryAdmin)
admin.site.register(Procedure)
admin.site.register(Simulation, SimulationAdmin)
admin.site.register(SelfEvaluation, SelfEvaluationAdmin)
#admin.site.register(Workspace)
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(Solution, SolutionAdmin)
admin.site.register(Book)
admin.site.register(Reference, ReferenceAdmin)
admin.site.register(Workspace)
admin.site.register(Contact)
admin.site.register(DefaultCode, DefaultCodeAdmin)
