import { createRouter, createWebHistory } from "vue-router"
import DashboardView from "../views/DashboardView.vue"
import PredictView from "../views/PredictView.vue"
import HistoryView from "../views/HistoryView.vue"
import AnalysisView from "../views/AnalysisView.vue"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "dashboard",
      component: DashboardView,
    },
    {
      path: "/predict",
      name: "predict",
      component: PredictView,
    },
    {
      path: "/history",
      name: "history",
      component: HistoryView,
    },
    {
      path: "/analysis",
      name: "analysis",
      component: AnalysisView,
    },
  ],
})

export default router
