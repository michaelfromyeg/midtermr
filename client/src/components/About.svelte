<svelte:head>
    <title>midtermr — about</title>
</svelte:head>

<div class="about">
    <h2>About</h2>
    <h3 class="subheader">What is midtermr?</h3>
    <p>
        <a
            href="https://github.com/michaelfromyeg/midtermr"
            target="_blank"
            rel="noreferrer"
            >midtermr
        </a>
        is a side project that aims to leverage
        <a
            href="https://personal.math.ubc.ca/~CLP/"
            target="_blank"
            rel="noreferrer"
            >CLP
        </a>
        textbook questions to generate customizable practice exams for Calculus I,
        II, and III. The CLP and midtermr were developed at The University of British
        Columbia (UBC) in Vancouver, Canada.
    </p>
    <p>
        Issues or bugs with the midtermr software may be reported to <a
            href="https://github.com/michaelfromyeg/midtermr/issues"
            target="_blank"
            rel="noreferrer">its GitHub repository</a
        >. Pull requests are welcome; the frontend web application is written in
        JavaScript (Svelte) and the backend is written in Python (Flask). The
        API is completely accessible; documentation to come.
    </p>
    <p>
        Full rights for CLP questions belong to its creators and maintainers (<a
            href="http://www.math.ubc.ca/~feldman/"
            target="_blank"
            rel="noreferrer">Joel Feldman</a
        >,
        <a
            href="http://www.math.ubc.ca/~andrewr/front_page.html"
            target="_blank"
            rel="noreferrer">Andrew Rechnitzer</a
        >
        and
        <a
            href="http://www.math.ubc.ca/~elyse/index.html"
            target="_blank"
            rel="noreferrer">Elyse Yeager</a
        >). Mistakes or issues with the content may be directed to their
        <a
            href="https://personal.math.ubc.ca/~CLP/Bounty"
            target="_blank"
            rel="noreferrer">Bug Bounty</a
        >.
    </p>
    <h3 class="subheader">How do I use it?</h3>
    <p>
        To generate an exam, head to the homepage and select your user settings.
        You may use one of many presets, as well.
    </p>
    <p>
        You will then be redirected to the exam page. It will also be saved in
        your list of past exams, which you can track on your homepage. Exams are
        also available for PDF download, after a short period of time.
    </p>
</div>

<style>
    .about {
        max-width: 70ch;
        margin: 0 auto;
    }

    .subheader {
        color: #888;
    }
</style>
