/* Copyright 2023 Marimo. All rights reserved. */
import { PlusIcon } from "lucide-react";
import { Button } from "@/editor/inputs/Inputs";
import { Tooltip } from "../../components/ui/tooltip";

export const CreateCellButton = ({
  appClosed,
  onClick,
  tooltipContent,
}: {
  appClosed: boolean;
  tooltipContent: React.ReactNode;
  onClick?: () => void;
}) => {
  return (
    <Tooltip content={tooltipContent} usePortal={false}>
      <Button
        onClick={onClick}
        className={`ShoulderButton ${appClosed ? " inactive-button" : ""}`}
        shape="circle"
        size="small"
        color="hint-green"
        data-testid="create-cell-button"
      >
        <PlusIcon strokeWidth={1.8} />
      </Button>
    </Tooltip>
  );
};
