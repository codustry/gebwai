<script context="module">
	export function preload() {
		return this.fetch(`blog.json`).then(r => r.json()).then(posts => {
			return { posts };
		});
	}
</script>

<script>
	export let posts;
</script>

<svelte:head>
	<title>บล็อก | Gebwai (เก็บไว้)</title>
</svelte:head>

<div class="inner-banner bg-default-2 pt-25 pt-lg-29 pb-10 pb-lg-10" id="pricing">
  <div class="container">
    <div class="row  justify-content-center pt-5">
      <div class="col-xl-8 col-lg-9">
        <div class="px-md-15 text-center mb-5 mb-lg-13">
          <h2 class="title mb-9 mb-lg-12">บก.เก็บไว้</h2>
          <p class="gr-text-8 mb-0">ไม่ว่าจะเป็นอะไรใหม่ๆ หรือ สาระความรู้ เราจะนำมาเขียนเล่าเรื่องราวให้พี่ๆอ่านกัน ที่นี่จะเป็นที่แรกสุดที่จะได้รับเรื่องราวใหม่ๆเกี่ยวกับผม</p>
        </div>
      </div>
    </div>
  </div>
</div>

<div style="padding-top: 50px"></div>

{#each posts as post}
<div class="content-section pt-5 pt-lg-10 pb-5 pb-lg-10 bg-default-6">
	<div class="container">
		<div class="row align-items-center justify-content-center">
			<div class="col-xs-11 col-sm-10 col-md-9 col-lg-6 col-xl-6 mb-6 mb-md-13 mb-lg-0">
			<div class="tel-content-image-group-1" data-aos="zoom-in" data-aos-duration="1200" data-aos-once="true">
				<!-- <div class="abs-image-1 responsive-scaling-2">
				<div class="animation-item">
					<img class="main-img" src="../image/telemedicine/png/content-1-img1.png"  alt="" id="an-item-2p1">
				</div>
				</div>
				<div class="abs-image-2 responsive-scaling-2">
				<div class="animation-item">
				<img class="main-img" src="../image/telemedicine/png/content-1-img2.png" alt="" id="an-item-2p2"/>
				</div>
				</div> -->
				<div class="gr-abs-center gr-z-index-n1">
					<img src={post.preview_image} alt="" class="responsive-scaling-2" height="350px">
				</div>
			</div>
			</div>
			<div class="col-sm-10 col-md-9 col-lg-6 col-xl-5 offset-xl-1">
			<div class="content-text pr-lg-10">
				<h2 class="gr-text-4 mb-9">{post.title}</h2>
				<p class="gr-text-9 mb-0">{post.preview_content}</p>
				<a rel="prefetch" href="blog/{post.slug}" class="btn-link with-icon gr-text-blue gr-text-9 font-weight-bold mt-10">อ่านต่อ<i class="fas fa-arrow-right"></i></a>
			</div>
			</div>
		</div>
	</div>
</div>
{/each}
