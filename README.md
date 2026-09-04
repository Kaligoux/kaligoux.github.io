A simple blog, no static-site framework/CMS, only HTML, CSS, JS, published with Github pages.

*structure*

--- .github/workflows/deploy.yml # build and deploys the site
--- posts/ # Blog posts
--- images/ # Images used by posts
--- index.html # Blog homepage
--- build.py # generates the final site (index.html) by taking all the blog posts and appending them in index.html.


#Local Development
- local preview in localhost:8000

run ./build.py
python3 -m http.server --directory dist 

#Deployment
Every push to main triggers the Github Actions workflow

1. Checks out the repo
2. runs ./build.py
3. uploads dist/ as a Github Pages artifact
4. Deploys the artifact to Github Pages

