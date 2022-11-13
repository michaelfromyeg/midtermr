<script>
    import { onMount } from "svelte";
    import { serverUrl } from "../../constants";

    export let examId;

    let content = "";
    let typsetting = true;

    onMount(async () => {
        // Set MathJax settings on global window object
        // @ts-ignore
        window.MathJax = {
            tex: {
                inlineMath: [
                    ["$", "$"],
                    ["\\(", "\\)"],
                ],
            },
            chtml: {
                displayAlign: "left",
            },
        };

        // Re-add scripts to head (...no idea why this works or is needed)
        [
            "https://polyfill.io/v3/polyfill.min.js?features=es6",
            "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js",
        ].forEach((script) => {
            const elt = document.createElement("script");
            elt.src = script;
            document.head.appendChild(elt);
        });

        try {
            const response = await fetch(`${serverUrl}/exams/${examId}`);
            const body = await response.json();

            content = body.content;

            // (I also have no idea why this needs to be wrapped in a setTimeout to work...)
            setTimeout(function () {
                // @ts-ignore
                MathJax.typeset();

                typsetting = false;
            }, 0);
        } catch (error) {
            console.error(error);
        }
    });
</script>

<svelte:head>
    <title>midtermr — exam</title>
</svelte:head>

<div class="exam">
    <h1 class="exam-title">Exam: {examId}</h1>
    {#if typsetting}
        <p class="exam-message">
            Processing exam <span class="latex"
                >L<sup>a</sup>T<sub>e</sub>X</span
            >...
        </p>
    {/if}

    <!-- Hide exam content while still being typeset, but still render on page to allow MathJax to work! -->
    <span style={typsetting ? "display: none" : ""}>
        {@html content}
    </span>
</div>

<style>
    .exam-title,
    .exam-message {
        text-align: center;
    }

    .latex sub,
    .latex sup {
        text-transform: uppercase;
    }

    .latex sub {
        vertical-align: -0.5ex;
        margin-left: -0.1667em;
        margin-right: -0.125em;
    }

    .latex,
    .latex sub {
        font-size: 1em;
    }

    .latex sup {
        font-size: 0.85em;
        vertical-align: 0.15em;
        margin-left: -0.36em;
        margin-right: -0.15em;
    }
</style>
