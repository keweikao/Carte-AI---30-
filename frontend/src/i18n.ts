import { getRequestConfig } from 'next-intl/server';

export default getRequestConfig(async ({ locale }) => {
    const currentLocale = locale || 'zh-TW';
    return {
        locale: currentLocale,
        messages: (await import(`../messages/${currentLocale}.json`)).default
    };
});
