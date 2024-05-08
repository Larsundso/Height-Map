import { SECRET } from '$env/static/private';
import DataBase from '$lib/server/database.js';
import { error, json } from '@sveltejs/kit';
import jwt from 'jsonwebtoken';
import ms from 'ms';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = async (req) => {
	const token = req.cookies.get('token');
	if (!token) return error(401, 'No Token');

	try {
		jwt.verify(token, SECRET);
	} catch (e) {
		return error(401, 'Token invalid');
	}

	const data = await DataBase.data.findMany({
  where: { timestamp: { lte: Math.abs(Date.now() - ms(req.url.searchParams.get('before') ?? '0m')) } },
		orderBy: { timestamp: 'desc' },
		take: Number(req.url.searchParams.get('take') ?? '25'),
	});

	return json(data);
};
