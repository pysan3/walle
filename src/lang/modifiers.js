const capitilize = (s) => {
  if (typeof s !== 'string') return '';
  return s && s.charAt(0).toUpperCase() + s.slice(1);
};

export default {
  snakeCase: (str) => str.split(' ').join('_'),
  camelCase: (str) => str.split(' ').map((e, i) => (i ? capitilize(e) : e)).join(''),
};
