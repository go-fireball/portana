// plugins/vuetify.ts

import { createVuetify } from 'vuetify'
import { md3 } from 'vuetify/blueprints'

import { aliases, mdi } from 'vuetify/iconsets/mdi-svg'
import {darkThemeColors, lightThemeColors} from "~/theme/theme";


export default defineNuxtPlugin(nuxtApp => {
    const vuetify = createVuetify({
        ssr: true,
        theme: {
            defaultTheme: 'light',
            themes: {
                light: {
                    colors: lightThemeColors,
                },
                dark: {
                    colors: darkThemeColors,
                },
            },
        },
        icons: {
            defaultSet: 'mdi',
            aliases,
            sets: {
                mdi,
            },
        },
        defaults: {
            global: {
                ripple: false,
            },
        },
        blueprint: md3, // or md2
    })

    nuxtApp.vueApp.use(vuetify)
})
