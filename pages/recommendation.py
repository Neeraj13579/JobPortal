from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

class SkillsBasedRecommendation:
    def __init__(self, job_posts):
        self.job_posts = job_posts
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.job_post_matrix = self.vectorizer.fit_transform(job_posts.values_list('skills_requirement', flat=True))  # Use values_list to get a flat list of skills_requirement values

    def recommend_jobs(self, user_profile, num_recommendations):
        user_profile_vector = self.vectorizer.transform([user_profile.skills])
        
        cosine_similarities = linear_kernel(user_profile_vector, self.job_post_matrix).flatten()
        
        job_indices = cosine_similarities.argsort()[::-1]
        
        
        job_posts_list = list(self.job_posts)
        recommended_jobs = [job_posts_list[i] for i in job_indices[:num_recommendations]]
        
        return recommended_jobs