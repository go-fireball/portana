import { defineNuxtPlugin } from "#app";
import pino from "pino";


export default defineNuxtPlugin(() => {
    const logger = pino({
        level: "info",
        browser: {
            asObject: true, // Logs structured data in the browser console
        },
    });

    return {
        provide: {
            logger,
        },
    };
});
