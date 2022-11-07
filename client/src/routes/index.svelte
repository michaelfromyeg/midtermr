<script>
    import { Router, Route } from "svelte-routing";
    import Home from "../components/Home.svelte";
    import About from "../components/About.svelte";
    import Exam from "../components/Exam.svelte";

    export let url = "";
</script>

<Router {url}>
    <div>
        <Route path="/exams/:examId" let:params={examId} component={Exam} />
        <Route path="/about" component={About} />
        <Route path="/" component={Home} />
    </div>
</Router>
