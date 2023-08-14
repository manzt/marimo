/* Copyright 2023 Marimo. All rights reserved. */
import parse, { Element } from "html-react-parser";
import React from "react";

interface Props {
  html: string;
}

/**
 * Wrapper for customer dangerouslySetInnerHTML.
 * We instead render HTML to React elements using html-react-parser as this keeps
 * React elements in place so React's reconciliation algorithm will update nodes instead of unmounting and remounting.
 */
export const RenderHTML: React.FC<Props> = ({ html }) => {
  return (
    <>
      {parse(html, {
        replace: (domNode) => {
          // For iframe, we just want to use dangerouslySetInnerHTML so:
          // 1) we can remount the iframe when the src changes
          // 2) keep event attributes (onload, etc.) since this library removes them
          if (
            domNode instanceof Element &&
            domNode.attribs &&
            domNode.name === "iframe"
          ) {
            const element = document.createElement("iframe");
            Object.entries(domNode.attribs).forEach(([key, value]) => {
              element.setAttribute(key, value as string);
            });
            return (
              <div dangerouslySetInnerHTML={{ __html: element.outerHTML }} />
            );
          }
          return domNode;
        },
      })}
    </>
  );
};
