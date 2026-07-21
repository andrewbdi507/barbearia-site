// ============================================================
// Design System — Public API
// Single entry point for all components, tokens, themes, hooks.
// ============================================================

// Utils
export { cn } from "./utils/cn";

// Tokens
export { tokens } from "./tokens";
export type { DesignTokens } from "./tokens";

// Themes
export { themes, applyTheme, getThemeById } from "./themes";
export type { Theme, ThemeColors } from "./themes";

// Theme Provider (React Context for dynamic theme switching)
export { ThemeProvider, useTheme, type ThemeProviderProps } from "./components/ThemeProvider";

// Components
export { Button, type ButtonProps } from "./components/Button";
export { Input, type InputProps } from "./components/Input";
export {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  CardFooter,
  CardStat,
  type CardProps,
} from "./components/Card";
export { Modal, type ModalProps } from "./components/Modal";
export { ToastProvider, useToast, type Toast } from "./components/Toast";
export {
  Badge,
  Avatar,
  Skeleton,
  EmptyState,
  Spinner,
  type BadgeProps,
  type AvatarProps,
  type SkeletonProps,
  type EmptyStateProps,
} from "./components/Display";
