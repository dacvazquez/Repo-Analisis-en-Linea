from TikTokApi import TikTokApi
api = TikTokApi()

results = 10

# Since TikTok changed their API you need to use the custom_verifyFp option. 
# In your web browser you will need to go to TikTok, Log in and get the s_v_web_id value.
trending = api.trending()

for tiktok in trending.videos():
    tiktok.author.videos()

print(len(trending))