document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('articleModal');
    const modalTitle = document.getElementById('modalTitle');
    const modalDate = document.getElementById('modalDate');
    const modalContent = document.getElementById('modalContent');
    const closeBtn = document.getElementsByClassName('close')[0];
    const blogList = document.getElementById('blog-list');
    const loadingDiv = document.getElementById('loading');
    let page = 1;
    const postsPerPage = 5; // Reduced number of posts per page
    let loading = false;
    let allPostsLoaded = false;

    const copyNotification = document.getElementById('copyNotification');

    function openModal(postId) {
        fetch(`/blog/${postId}/content`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                modalTitle.textContent = data.title;
                modalDate.textContent = data.date;
                modalContent.innerHTML = data.content; // This line remains the same
                modal.style.display = 'block';
                document.body.style.overflow = 'hidden';
                history.replaceState(null, '', `/blog/${postId}`);

                // Add this: Parse and execute any script tags in the content
                const scripts = modalContent.getElementsByTagName('script');
                for (let script of scripts) {
                    eval(script.innerHTML);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error loading the article. Please try again.');
            });
    }

    function loadPosts() {
        if (loading || allPostsLoaded) return;
        loading = true;
        loadingDiv.style.display = 'block';

        fetch(`/blog/posts?page=${page}&per_page=${postsPerPage}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.posts.length === 0) {
                    allPostsLoaded = true;
                    loadingDiv.textContent = 'No more posts to load.';
                    return;
                }
                data.posts.forEach(post => {
                    const postElement = createPostElement(post);
                    blogList.appendChild(postElement);
                });
                page++;

                if (blogList.children.length >= data.total_posts) {
                    allPostsLoaded = true;
                    loadingDiv.textContent = 'All posts loaded.';
                } else {
                    loadingDiv.textContent = `Showing ${blogList.children.length} of ${data.total_posts} posts`;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                loadingDiv.textContent = 'Error loading posts. Please try again.';
            })
            .finally(() => {
                loading = false;
                loadingDiv.style.display = allPostsLoaded ? 'none' : 'block';
            });
    }

    function createPostElement(post) {
        const article = document.createElement('article');
        article.className = 'blog-card';
        article.dataset.postId = post.filename;

        article.innerHTML = `
            <div class="blog-card-inner">
                ${post.image ? `<div class="blog-card-image" style="background-image: url('${post.image}')"></div>` : ''}
                <div class="blog-card-content">
                    <div class="blog-card-title-container">
                        <h2 class="blog-card-title">${post.title}</h2>
                        <i class="fas fa-link blog-card-copy-link" title="Copy link to post"></i>
                    </div>
                    <p class="blog-card-date">${post.date}</p>
                    <div class="blog-card-description">
                        ${post.description || post.content.substring(0, 150) + '...'}
                    </div>
                    <button class="blog-card-read-more">Read More</button>
                </div>
            </div>
        `;

        // Make title clickable
        article.querySelector('.blog-card-title').addEventListener('click', function(e) {
            e.preventDefault();
            openModal(post.filename);
        });

        // Make image clickable if it exists
        const imageElement = article.querySelector('.blog-card-image');
        if (imageElement) {
            imageElement.addEventListener('click', function(e) {
                e.preventDefault();
                openModal(post.filename);
            });
        }

        // Keep the "Read More" button clickable
        article.querySelector('.blog-card-read-more').addEventListener('click', function(e) {
            e.preventDefault();
            openModal(post.filename);
        });

        // Add copy link functionality
        article.querySelector('.blog-card-copy-link').addEventListener('click', function(e) {
            e.preventDefault();
            const postUrl = `${window.location.origin}/blog/${post.filename}`;
            navigator.clipboard.writeText(postUrl).then(() => {
                showCopyNotification();
            }).catch(err => {
                console.error('Failed to copy link: ', err);
            });
        });

        return article;
    }

    function showCopyNotification() {
        copyNotification.classList.add('show');
        setTimeout(() => {
            copyNotification.classList.remove('show');
        }, 2000); // Notification disappears after 2 seconds
    }

    closeBtn.onclick = function() {
        modal.style.display = 'none';
        document.body.style.overflow = '';
        history.pushState(null, '', '/blog');
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
            document.body.style.overflow = '';
            history.pushState(null, '', '/blog');
        }
    }

    window.addEventListener('popstate', function() {
        if (modal.style.display === 'block') {
            modal.style.display = 'none';
            document.body.style.overflow = '';
        } else if (window.location.pathname.startsWith('/blog/')) {
            const postId = window.location.pathname.split('/').pop();
            openModal(postId);
        }
    });

    window.addEventListener('scroll', () => {
        if (!allPostsLoaded && window.innerHeight + window.scrollY >= document.body.offsetHeight - 500) {
            loadPosts();
        }
    });

    // Initial load
    loadPosts();

    // Check if there's a specific post to open
    const pathParts = window.location.pathname.split('/');
    if (pathParts.length > 2 && pathParts[1] === 'blog') {
        const postId = pathParts[2];
        openModal(postId);
    }
});