# Connection String URLs

# Language codes  ..
lang_codes = {"english":"1", "hindi":"6"}

# Curriculum API URLs ..
base_url = "https://v3cdemo.vridhee.com/webapigateway"

get_sub_url = base_url + '/api/v1/ai/curriculum_dashboard_module_ms/getSubjectsList'
add_sub_url = base_url + '/api/v1/ai/curriculum_dashboard_module_ms/insertSubjects'
update_sub_curr_url = base_url + "/api/v1/ai/curriculum_dashboard_module_ms/updateCurrCategory"

get_curr_types_url = base_url + '/api/onboarding/getCurriculumTypes'
get_grade_url = base_url + '/api/onboarding/getGradesdropdown?_id='

add_sub_chap_url = base_url + "/api/v1/ai/curriculum_dashboard_module_ms/addSubjectChapter"
get_sub_chap_url = base_url + "/api/v1/ai/curriculum_dashboard_module_ms/getSubjectChapter?subject_id="

add_topics_url = base_url + "/api/v1/ai/curriculum_dashboard_module_ms/addTopics/"
get_topics_url = base_url + "/api/v1/ai/curriculum_dashboard_module_ms/getTopics/"

# Getting Subject-wise Grades list API ..
grade_list_url = base_url + "/api/onboarding/getGradesdropdown?subject={subject_name}&gradeSection=grades"

# Content dumping URLs ..
api_url = "http://demoapi.vridhee.com:3010"

# English URLs ..
add_ai_url = api_url + "/api/v1/ai/curriculum_dashboard_module_ms"

