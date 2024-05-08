<script lang="ts">
	import '$lib/scripts/index.js';
</script>

<div
	id="main"
	class="of-hidden flex flex-col justify-between items-center min-h-full text-center break-normal select-none min-w-100vw bg-gradient-linear bg-gradient-[142deg,rgba(0,0,0,1)_0%,rgba(98,14,14,1)_73%] bg-[100%100%]
 before:block before:h-60vh before:left-0 before:top-0 before:z-0 before:w-100vw before:fixed before:pointer-events-none before:bg-center before:bg-no-repeat before:bg-scroll before:scale-100 before:bg-[100%100%] before:h-60vh before:pointer-events-none before:fixed
  after:bg-black after:block after:h-full after:left-0 after:opacity-0 after:fixed after:scale-100 after:top-0 after:transition-opacity after:duration-1s after:ease-in-out after:delay-0.25s after:transition-visibility after:delay-1s after:delay-0.25s after:invisible after:w-full"
>
	<content class="mx-2 z-1 w-full max-w-100%">
		<slot />
	</content>
</div>
