import Markdown from "react-markdown";

export interface MessageTextProps {
  content: string;
}

export function AIMessageText(props: MessageTextProps) {
  return (
    <div className="flex mr-auto w-fit max-w-[700px] bg-gradient-to-r from-green-600 to-green-700 rounded-md px-2 py-1 mt-3 shadow-lg">
      <div className="text-normal text-gray-50 text-left break-words">
        <Markdown>{props.content}</Markdown>
      </div>
    </div>
  );
}

export function HumanMessageText(props: MessageTextProps) {
  return (
    <div className="flex ml-auto w-fit max-w-[700px] bg-gray-200 rounded-md px-2 py-1 shadow-lg">
      <div className="text-normal text-gray-800 text-left break-words">
        {props.content}
      </div>
    </div>
  );
}
