import httpProxy from 'express-http-proxy';
import { proxyConfig } from './proxy';

export const AuthRoute = httpProxy(process.env.AUTH_URL, proxyConfig);
export const AccountRoute = httpProxy(process.env.ACCOUNT_URL, proxyConfig);
export const EventRoute = httpProxy(process.env.EVENT_URL, proxyConfig);
