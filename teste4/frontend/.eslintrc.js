export const root = true;
export const env = {
    node: true,
};
export const extendsConfig = [
    'plugin:vue/vue3-essential',
    'eslint:recommended',
];
export const parserOptions = {
    parser: '@babel/eslint-parser',
};
export const rules = {
    'vue/multi-word-component-names': 'off',
    'vue/no-unused-vars': 'off',
    'vue/no-multiple-template-root': 'off',
    'vue/valid-v-slot': 'off',
    'vue/no-v-model-argument': 'off',
    'no-unused-vars': [
        'error',
        {
            vars: true,
            args: 'after-used',
            ignoreRestSiblings: true
        }
    ],
};