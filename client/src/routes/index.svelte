<script>
    import { Router, Route } from "svelte-routing";
    import Home from "../components/Home.svelte";
    import About from "../components/About.svelte";
    import Exam from "../components/Exam.svelte";
    import Header from "../components/Header.svelte";
    import Footer from "../components/Footer.svelte";

    export let url = "";
</script>

<Router {url}>
    <Header />
    <div>
        <Route path="/exams/:examId" let:params={examId} component={Exam} />
        <Route path="/about" component={About} />
        <Route path="/" component={Home} />
    </div>
    <Footer />
</Router>
