import type { NextRequest } from 'next/server';
import { NextResponse } from 'next/server';
import createMiddleware from 'next-intl/middleware';

const supportedLocales = ['en', 'zh-TW'] as const;
const defaultLocale = 'zh-TW';

// Map common/legacy locale slugs back to supported locales to avoid bad redirects
const localeAliases: Record<string, string> = {
    zh: 'zh-TW',
    'zh-tw': 'zh-TW',
    zn: 'zh-TW'
};

const normalizeLocale = (slug?: string | null): string | undefined => {
    if (!slug) return undefined;
    const lower = slug.toLowerCase();
    if (localeAliases[lower]) return localeAliases[lower];
    if (supportedLocales.includes(slug as (typeof supportedLocales)[number])) return slug;
    if (supportedLocales.includes(lower as (typeof supportedLocales)[number])) return lower;
    return undefined;
};

const intlMiddleware = createMiddleware({
    locales: supportedLocales as unknown as string[],
    defaultLocale,
    localePrefix: 'as-needed',
    localeDetection: true,
    alternateLinks: true
});

export default function middleware(request: NextRequest) {
    const url = request.nextUrl.clone();
    const originalPathname = url.pathname;
    const segments = originalPathname.split('/').filter(Boolean);
    const first = segments[0];
    const second = segments[1];
    const normalizedFirst = normalizeLocale(first);
    const normalizedSecond = normalizeLocale(second);

    // Fix malformed locale nesting such as /en/zh → /zh-TW
    if (normalizedFirst && normalizedSecond) {
        segments.splice(0, 2, normalizedSecond);
    } else if (normalizedFirst && first !== normalizedFirst) {
        // Fix alias in first segment (e.g., /zh or /zn -> /zh-TW)
        segments[0] = normalizedFirst;
    } else if (!normalizedFirst && localeAliases[first?.toLowerCase() || '']) {
        // Alias without proper casing detected, normalize
        segments[0] = localeAliases[first!.toLowerCase()];
    }

    // Build target path and detect if redirect is needed
    const targetPathname = `/${segments.join('/')}`;
    const needRedirect = targetPathname !== originalPathname;

    // Normalize locale stored in cookie (old "zh" might produce broken paths like /en/zh/input)
    const cookieLocale = request.cookies.get('NEXT_LOCALE')?.value;
    const normalizedCookieLocale = normalizeLocale(cookieLocale) || defaultLocale;
    const needCookieUpdate = cookieLocale !== normalizedCookieLocale;

    if (needRedirect) {
        url.pathname = targetPathname.replace(/\/+/g, '/');
        const response = NextResponse.redirect(url);
        if (needCookieUpdate) {
            response.cookies.set('NEXT_LOCALE', normalizedCookieLocale);
        }
        return response;
    }

    // Let next-intl handle routing; also refresh cookie if needed without redirect
    const response = intlMiddleware(request);
    if (needCookieUpdate) {
        response.cookies.set('NEXT_LOCALE', normalizedCookieLocale);
    }
    return response;
}

export const config = {
    // Match all pathnames except for
    // - … if they start with `/api`, `/_next` or `/_vercel`
    // - … the ones containing a dot (e.g. `favicon.ico`)
    matcher: ['/((?!api|_next|_vercel|.*\\..*).*)']
};
