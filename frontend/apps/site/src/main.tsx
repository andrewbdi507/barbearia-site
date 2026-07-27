import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { HelmetProvider } from "react-helmet-async";
import { ThemeProvider, ToastProvider } from "@barbershop/design-system";
import { ThemeProvider as SiteThemeProvider } from "./themes/ThemeProvider";
import App from "./App";
import "./styles/globals.css";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { staleTime: 30_000, retry: 1, refetchOnWindowFocus: false },
  },
});

const helmetContext = {};

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <HelmetProvider context={helmetContext}>
      <SiteThemeProvider>
        <ThemeProvider defaultTheme="urban">
          <QueryClientProvider client={queryClient}>
            <BrowserRouter>
              <ToastProvider>
                <App />
              </ToastProvider>
            </BrowserRouter>
          </QueryClientProvider>
        </ThemeProvider>
      </SiteThemeProvider>
    </HelmetProvider>
  </React.StrictMode>
);
