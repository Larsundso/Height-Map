<script lang="ts">
	import type { PageData } from './$types';
	import { Line } from 'svelte-chartjs';
	import {
		Chart as ChartJS,
		Title,
		Tooltip,
		Legend,
		LineElement,
		LinearScale,
		PointElement,
		CategoryScale,
		type Point,
		type ChartData,
	} from 'chart.js';
	import { onDestroy, onMount } from 'svelte';

	export let data: PageData;
	let show: typeof data.stats;
	$: show = data.stats.reverse();
	let take: number;
	$: take = 25;
 let before: string;
 $: before = '0m';

	const baseDatasetOpts: Omit<
		ChartData<'line', (number | Point)[], unknown>['datasets'][number],
		'data'
	> = {
		fill: true,
		backgroundColor: 'rgba(225, 204,230, .3)',
		borderCapStyle: 'butt',
		borderDash: [],
		borderDashOffset: 0.0,
		borderJoinStyle: 'miter',
		pointBorderColor: 'rgb(205, 130,1 58)',
		pointBackgroundColor: 'rgb(255, 255, 255)',
		pointBorderWidth: 10,
		pointHoverRadius: 5,
		pointHoverBackgroundColor: 'rgb(0, 0, 0)',
		pointHoverBorderColor: 'rgba(220, 220, 220,1)',
		pointHoverBorderWidth: 2,
		pointRadius: 1,
		pointHitRadius: 10,
	};

	const getLabel = (): ChartData<'line', (number | Point)[], unknown>['labels'] =>
		show?.map((d) => {
			const date = new Date(Number(d.timestamp));
			const hours = String(date.getHours()).padStart(2, '0');
			const minutes = String(date.getMinutes()).padStart(2, '0');
			const seconds = String(date.getSeconds()).padStart(2, '0');
			return `${hours}:${minutes}:${seconds}`;
		});

	const getDatasets = (): ChartData<'line', (number | Point)[], unknown>['datasets'] => [
		{
			...baseDatasetOpts,
			borderColor: 'red',
			label: 'Altitude',
			data: show?.map((d) => Number(d.height)),
		},
		{
			...baseDatasetOpts,
			borderColor: 'blue',
			label: 'Humidity',
			data: show?.map((d) => Number(d.humidity)),
		},
		{
			...baseDatasetOpts,
			borderColor: 'green',
			label: 'Pressure',
			data: show?.map((d) => Number(d.pressure)),
		},
		{
			...baseDatasetOpts,
			borderColor: 'yellow',
			label: 'Temperature',
			data: show?.map((d) => Number(d.temperature)),
		},
	];

	let chartData: ChartData<'line', (number | Point)[], unknown>;
	$: chartData = {
		labels: getLabel(),
		datasets: getDatasets(),
	};

	let interval: NodeJS.Timeout;
	onMount(() => {
		interval = setInterval(async () => {
			show = (
				await fetch(`/api/data?take=${take}&before=${before}`).then((r) => r.json() as Promise<typeof data.stats>)
			).reverse();

			chartData = {
				labels: getLabel(),
				datasets: getDatasets(),
			};

			ChartJS.register(Title, Tooltip, Legend, LineElement, LinearScale, PointElement, CategoryScale);
		}, 5000);
	});

	onDestroy(() => {
		clearInterval(interval);
	});

	ChartJS.register(Title, Tooltip, Legend, LineElement, LinearScale, PointElement, CategoryScale);
</script>

<button
	class="absolute right-2 top-2 bg-neutral-800 px-4 py-2 hover:bg-neutral-600"
	on:click={() => fetch('/api/logout', { method: 'POST' }).then(() => window.location.reload())}
>
	Log Out
</button>

<form class="flex flex-col justify-center items-center text-center my-5">
	<label for="take" class="text-center">Menge der Einträge</label>
	<input type="number" name="take" class="text-center" bind:value={take} />
 
	<label for="before" class="text-center">Vor</label>
	<input type="text" name="before" class="text-center" bind:value={before} />
</form>

<div class="flex flex-row justify-center items-center gap-2 w-full flex-wrap">
	{#each chartData.datasets as d}
		<div class="w-45%">
			<Line
				data={{ labels: chartData.labels, datasets: [d] }}
				options={{ responsive: true, animation: false }}
				class="m-auto border-1px border-solid border-white w-full"
			/>
		</div>
	{/each}
</div>
