import ReactMarkdown from "react-markdown";

function ResultCard({ answer }) {
  return (
    <div className="bg-white rounded-xl shadow-sm border-l-4 border-emerald-500 p-6">
      <h2 className="text-lg font-semibold text-slate-700 mb-3">📊 AI 분석 결과</h2>
      {/* 기존 <p> 태그 대신 ReactMarkdown을 사용하여 
        마크다운 문법을 HTML 태그(h3, strong 등)로 안전하게 파싱합니다.
      */}
      <div className="text-slate-600 text-sm leading-relaxed markdown-body">
        <ReactMarkdown>{answer}</ReactMarkdown>
      </div>
    </div>
  );
}

export default ResultCard;