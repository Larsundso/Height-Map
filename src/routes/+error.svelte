<script lang="ts">
	import FancyBorder from '$lib/components/generic/FancyBorder.svelte';
	import { page } from '$app/stores';
	import { invalidateAll } from '$app/navigation';
	import { redirect } from '@sveltejs/kit';
	import { onMount } from 'svelte';

	onMount(async () => {
		const reload = $page.url.searchParams.get('reload');
		if (!reload) return;

		await invalidateAll();
		redirect(307, '/');
	});
</script>

<div class="flex flex-col items-center">
	<h1 class="text-xl mt-2">I think you got lost :c</h1>

	<span class="mt-2">The page you were looking for, doesn't exist</span>

	<FancyBorder />

	<a href="/" class="btn-medium mt-2">Take me back</a>
</div>
