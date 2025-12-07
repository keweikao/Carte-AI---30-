import createMiddleware from 'next-intl/middleware';

export default createMiddleware({
    // A list of all locales that are supported
    locales: ['en', 'zh-TW', 'zh'],

    // Used when no locale matches
    defaultLocale: 'zh-TW',

    // Locale detection and alias mapping
    localePrefix: 'as-needed',

    // Map 'zh' to 'zh-TW' for backwards compatibility
    localeDetection: true,
    alternateLinks: true
});

export const config = {
    // Match all pathnames except for
    // - … if they start with `/api`, `/_next` or `/_vercel`
    // - … the ones containing a dot (e.g. `favicon.ico`)
    matcher: ['/((?!api|_next|_vercel|.*\\..*).*)']
};
