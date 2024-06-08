<script>
	import { dev } from '$app/environment';
	import { page } from '$app/stores';
</script>

<h1>404</h1>

{#if dev}
	<p>See console for details.</p>
	<pre>{JSON.stringify($page)}</pre>
{:else}
	<p><a href="/">Go home</a></p>
{/if}
