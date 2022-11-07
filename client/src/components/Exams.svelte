<script>
    export let exams;
</script>

<section>
    <ul>
        {#each exams as exam}
            <li><a href="/exams/{exam.name}">{exam.name}</a></li>
        {/each}
    </ul>
</section>
