import reflex as rx


def get_main_styles():
    return rx.el.style(
        """
@tailwind base;
@tailwind components;
@tailwind utilities;

@import url('https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600;700;800&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Source+Code+Pro:wght@400;500&display=swap');

:root {
    --font-instrument-sans: 'Instrument Sans', sans-serif;
    --font-source-code-pro: 'Source Code Pro', monospace;
    --shadow-small: 0px 2px 4px 0px rgba(28, 32, 36, 0.05);
    --shadow-medium: 0px 4px 8px 0px rgba(28, 32, 36, 0.04);
    --shadow-large: 0px 24px 12px 0px rgba(28, 32, 36, 0.02), 0px 8px 8px 0px rgba(28, 32, 36, 0.02), 0px 2px 6px 0px rgba(28, 32, 36, 0.02);
    .font-small {
        font-family: var(--font-instrument-sans);
        font-size: 0.9rem;
        font-style: normal;
        font-weight: 500;
        line-height: 1.25rem;
        letter-spacing: -0.01094rem;
    }
    .font-md {
        font-family: var(--font-instrument-sans);
        font-size: 1.125rem;
        font-style: normal;
        font-weight: 500;
        line-height: 1.625rem;
        letter-spacing: -0.01688rem;
    }
    .font-smbold {
        font-family: var(--font-instrument-sans);
        font-size: 1rem;
        font-style: normal;
        font-weight: 600;
        line-height: 1.5rem;
        letter-spacing: -0.015rem;
    }
    .font-base {
        font-family: var(--font-instrument-sans);
        font-size: 1rem;
        font-style: normal;
        font-weight: 500;
        line-height: 1.5rem;
        letter-spacing: -0.015rem;
    }
    .font-large {
        font-family: var(--font-instrument-sans);
        font-size: 1.5rem;
        font-weight: 600;
        line-height: 2rem;
        letter-spacing: -0.03rem;
    }
    .font-x-large {
        font-family: var(--font-instrument-sans);
        font-size: 2rem;
        font-style: normal;
        font-weight: 600;
        line-height: 2.5rem;
        letter-spacing: -0.06rem;
    }
    .font-xxx-large {
        font-family: var(--font-instrument-sans);
        font-size: 3.5rem;
        font-style: normal;
        font-weight: 600;
        line-height: 4rem;
        letter-spacing: -0.175rem;
    }
    .font-code {
        font-family: var(--font-source-code-pro);
        font-size: 0.875rem;
        font-style: normal;
        font-weight: 400;
        line-height: 1.5;
        letter-spacing: -0.01313rem;
    }
    .code-block {
        width: 100% !important;
        height: auto !important;
        margin: 0 !important;
        padding: 1rem !important;
        max-height: 350px !important;
        border-radius: 0.75rem !important;
        border: 1px solid var(--slate-5) !important;
        background: var(--white-1) !important;
        color: var(--slate-12) !important;
        resize: none !important;
        outline: none !important;
        scrollbar-width: thin !important;
        font-family: var(--font-source-code-pro) !important;
    }
    .code-block > * {
        background: transparent !important;
        font-family: var(--font-source-code-pro) !important;
        font-size: 0.875rem !important;
        font-style: normal !important;
        font-weight: 400 !important;
        line-height: 1.5 !important;
        letter-spacing: -0.01313rem !important;
    }
    .scrollbar-width-thin {
        scrollbar-width: thin;
    }
    .transition-color {
        transition: color 0.035s ease-out;
    }
    .transition-bg {
        transition: background-color 0.075s ease-out;
    }
}

@layer components {
    .font-instrument-sans {
        font-family: var(--font-instrument-sans);
    }
    .font-source-code-pro {
        font-family: var(--font-source-code-pro);
    }
    .shadow-large {
        box-shadow: var(--shadow-large);
    }
    .shadow-medium {
        box-shadow: var(--shadow-medium);
    }
    .shadow-small {
        box-shadow: var(--shadow-small);
    }
}

.light,
.light-theme {
	--white-1: #ffffff;
}

.dark,
.dark-theme {
	--white-1: #0E0F10;
}
"""
    )
