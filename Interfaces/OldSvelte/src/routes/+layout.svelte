<script>
	import Header from '$lib/components/Header.svelte';
	import Footer from '$lib/components/Footer.svelte';
</script>

<svelte:head>
	<title>Gebwai (เก็บไว้)</title>
	<script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
	<meta property="og:title" content="Gebwai (เก็บไว้)" />
	<meta
		property="og:description"
		content="เก็บรูป วิดีโอ และไฟล์ต่างๆ จากแชทไลน์ ไว้บน คลาว์ด โดยอัตโนมัติ"
	/>
	<meta property="og:url" content="https://www.gebwai.com" />
	<meta
		property="og:image"
		content="https://ik.imagekit.io/tqbc8pye197/webapp/blog-preview-1.png?tr=q-50"
	/>
</svelte:head>

<!-- <Nav {segment}/> -->
<Header />
<main>
	<slot />
</main>
<Footer />
