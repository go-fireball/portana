// ~/theme/theme.ts
export const lightThemeColors = {
    primary: '#4D8FE2',

    secondary: '#6C63FF',
    accent: '#FFD166',
    error: '#EF476F',
    info: '#118AB2',
    success: '#06D6A0',
    warning: '#FFB703',
    background: '#FAFAFA',
    surface: '#FFFFFF',

    // Soft background variants
    lightCream: '#FFF8F0',
    infoLight: '#E3F2FD',
    warningLight: '#FFF3E0',
    successLight: '#E8F5E9',
    primaryLight: '#E3F0FF', // Light variant of your primary (#4D8FE2)
    secondaryLight: '#F3E5F5',
};

export const darkThemeColors = {
    primary: '#4D8FE2',       // Same as light for brand consistency

    secondary: '#6C63FF',     // Same for continuity
    accent: '#FFD166',        // Same, works well on dark too
    error: '#EF476F',         // Slightly bright but consistent
    info: '#118AB2',          // Keeps tone, just as readable
    success: '#06D6A0',       // Matches light theme
    warning: '#FFB703',       // Same golden hue
    background: '#121212',    // Deep gray for contrast
    surface: '#1E1E1E',       // Elevated surfaces slightly lighter

    // Soft background variants adjusted for dark mode
    lightCream: '#2C2C2C',     // Neutral dark cream tone
    infoLight: '#1E2A33',      // Darkened version of info light
    warningLight: '#332B1A',   // Warm muted amber tone
    successLight: '#1A332A',   // Muted teal background
    primaryLight: '#1E2A3A', // Muted navy-blue tone for dark mode
    secondaryLight: '#241A33', // Muted purple base
};
