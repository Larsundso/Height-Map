import type { data as Data } from '@prisma/client';
import type { PageServerLoad } from './$types';
import { redirect } from '@sveltejs/kit';

export const load: PageServerLoad = async (event) => {
	const token = event.cookies.get('token');
	if (!token) return redirect(307, '/login');

	const res = await event.fetch('/api/data?take=25').then((r) => r.json() as Promise<Data[]>);

	return { stats: res };
};
