/* eslint-disable no-unused-vars */
import { createI18n } from 'vue-i18n';
import modifiers from '@/lang/modifiers';
import messages from '@/lang/dictionary.json';

const defaultDatetimeFormat = {
  date: { month: 'short', day: 'numeric' },
  short: { year: 'numeric', month: 'short', day: 'numeric' },
  year: { year: 'numeric' },
};

/* eslint-disable */
const locale = (
  (window.navigator.languages && window.navigator.languages[0]) ||
  window.navigator.language ||
  window.navigator.userLanguage ||
  window.navigator.browserLanguage
).includes('ja')
  ? 'ja'
  : 'en';
/* eslint-enable */

export default createI18n({
  legacy: true,
  locale,
  fallbackLocale: 'ja',
  messages,
  modifiers,
  datetimeFormats: Object.fromEntries(Object.keys(messages).map((lang) => [lang, defaultDatetimeFormat])),
});
